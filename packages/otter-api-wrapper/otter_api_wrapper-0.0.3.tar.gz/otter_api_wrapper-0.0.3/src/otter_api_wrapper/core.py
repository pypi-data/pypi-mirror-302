import pandas as pd
import requests
import json
import os
import time

class OtterAPI(object):
    def __init__(self,
                 api_token=None,
                 base_api_url="https://otter.ccm.sickkids.ca/api",
                 base_app_url="https://otter.ccm.sickkids.ca/app"
    ):
        self.api_token = api_token
        self.base_api_url = base_api_url
        self.base_app_url = base_app_url
        self.headers = {'Authorization': 'Bearer {}'.format(self.api_token)}


    def run_sample_path(
            self, file_path, model_name, atlas_version=None, sample_name=None, share_with=None,
            wait_for_result=True, timeout=300
        ):
        if sample_name is None:
            sample_name = file_path.split('/')[-1]
        df = pd.read_csv(file_path, sep='\t')
        return self.run_sample(
            df, model_name, atlas_version, sample_name, share_with,
            wait_for_result, timeout
        )
    
    def run_sample(
            self, df, model_name, atlas_version, sample_name, share_with,
            wait_for_result=True, timeout=1
        ):
        df = df.to_dict(orient='list')
        post_data = {'version': 'otter', 'data': df, 'name': sample_name}
        if share_with is not None:
            post_data['share_with'] = share_with
        r = requests.post(os.path.join(self.base_api_url, 'inference'), json=post_data, headers=self.headers)

        if r.status_code == 200:
            res = json.loads(r.text)

            if wait_for_result:
                return self.wait_for_sample(res['task_id'], timeout), res['inference_id']
            else:
                return res['task_id'], res['inference_id']
        else:
            raise Exception('Error in submitting inference job')


    def wait_for_sample(self, task_id, timeout):
        inference_link = 'inference_check?task_id={}'.format(task_id)
        request_link = os.path.join(self.base_api_url, inference_link)

        start = time.time()
        
        while True:
            r_check = requests.get(request_link, headers=self.headers)
        
            if r_check.status_code == 200:
                # Worked
                res_check = json.loads(r_check.text)
                if res_check['position'] is None:
                    # Finished running
                    df_check = pd.DataFrame.from_dict(res_check['result'])
                    return df_check
            else:
                raise Exception('Error in checking inference status')
            
            if time.time() - start > timeout:
                raise Exception('Timeout in waiting for inference result')

            time.sleep(1)


    def plot_sample(self, df_result, width=800, height=800):
        # df_result = df_result.apply(lambda x: round(x, 2))
        params = {
            'result': json.dumps(df_result.to_dict(orient='list')),
            'width': width,
            'height': height
        }

        r_plot = requests.post(os.path.join(self.base_app_url, 'plot_result'), json=params, headers=self.headers)
        
        if r_plot.status_code == 200:
            return json.loads(r_plot.json())
        else:
            raise Exception('Error in plotting result')
        
    def get_explore_plots(self, class_name=None):
        data = {
            'label': class_name
        }

        r_plot = requests.get(os.path.join(self.base_app_url, 'get_explore_plots'), params=data, headers=self.headers)
        print(r_plot.url)
        if r_plot.status_code == 200:
            return json.loads(r_plot.json())
        else:
            raise Exception('Error in getting explore plots')
        
    def download_pdf_report(self, inference_id, file_path):
        data = {
            'inference_id': inference_id
        }

        r_report = requests.get(os.path.join(self.base_api_url, 'download_pdf_result'), params=data, headers=self.headers)
        if r_report.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(r_report.content)
        else:
            raise Exception('Error in downloading pdf report')
        
        
        