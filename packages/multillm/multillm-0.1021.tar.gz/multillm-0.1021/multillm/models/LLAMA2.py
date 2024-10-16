# ==============================================================================
# Copyright 2023 VerifAI All Rights Reserved.
# https://www.verifai.ai
# License: 
#
# ==============================================================================
import os,sys
import json
import requests
from multillm.BaseLLM import BaseLLM
from multillm.Prompt import Prompt



# LLAMA-2 interface
"""
The LAMMA class extends the BaseModel class and overrides the get_response() method, providing an implementation.
The get_response() method takes a response parameter and returns the content of the first response in the given response object.
Llama 2
From Meta

Welcome to the official Hugging Face organization for Llama 2 models from Meta! In order to access models here, please visit the Meta website and accept our license terms and acceptable use policy before requesting access to a model. Requests will be processed within 1-2 days.

Llama 2 is a collection of pretrained and fine-tuned generative text models ranging in scale from 7 billion to 70 billion parameters. Our fine-tuned LLMs, called Llama-2-Chat, are optimized for dialogue use cases. Llama-2-Chat models outperform open-source chat models on most benchmarks we tested, and in our human evaluations for helpfulness and safety, are on par with some popular closed-source models like ChatGPT and PaLM.

Read our paper, learn more about the model, or get started with code on GitHub.

https://ai.meta.com/llama/
"""

class LLAMA2(BaseLLM):
    

    #implement here
    def __init__ (self, **kwargs):

       
        # add values here directly or if kwargs are specified they are taken from the config file
        defaults  = {
            "class_name" : "LLAMA2",
            "model" : "meta-llama/Llama-2-7b-chat-hf",
            "credentials" : "key.json"
        }
       
        
    
    # Get Text
    def get_content(self, response):
    
        """ Get the text from the response of an LLM """
        try:
            resp = response["generated_text"]
        except Exception as e:
            #print("error is_code() {0}" .format(str(e)))
            return('your prompt returned no response  as {}'.format(e))

        try:
            if self.is_code(resp):
                print("{0} response: {1}" .format(self.__class__.__name__,str(resp)))
                return str(resp), True
            else:
                return str(resp), False
        except Exception as e:
            #print("error is_code() {0}" .format(str(e)))
            return('LLAMA2 response failed as {}'.format(e))
        
    
    
    def get_response(self, prompt: Prompt, taskid=None, convid = None):
        
        
        """Predict using a Large Language Model."""
        project_id = "llama2"
        location = "us-central1"
        #url = "http://localhost/llama2/predict"

        if self.url is not None:
            url = self.url
        else:
            url = "http://localhost/llama2-vllm"

        
        """ Get credentials file set in the config, and set appropriate variables for your model """

        try:
            """ Call API """

            ## See if we can invoke importToDb
            headers = {"Content-Type" :  "application/json"}
            prmpt = prompt.get_string() + " , please return response in markdown format"
            context = ""
            if convid:
                qa = super().get_conversation_history(convid,"LLAMA2")
                for q,a in qa:
                    context += q + " " + a 
                cntx = "<<SYS>>" + context +"<</SYS>>"
                context = cntx + "\n[INST]" + prmpt + "[/INST]"
                prmpt = context
                
            if prompt.context:
                cntx = "<<SYS>>" + prompt.get_context() +"<</SYS>>"
                cntx += "\n" + prmpt
                prmpt = cntx
            #values = {'question':  prmpt}

            """ vllm server
        http://54.190.15.83/llama2-vllm     -H "Content-Type: application/json"
           -d '{ "model": "meta-llama/Llama-2-7b-chat-hf", "prompt": "write verilog code for a 4 port 16 entry FIFO controllers", "max_tokens":4096}'

            """
            values = {'prompt':  prmpt, "model" : "meta-llama/Llama-2-7b-chat-hf", "max_tokens":4096}
      
            resp = requests.post(url, data=json.dumps(values),headers=headers)
            #print("LLAMA2 Response: {0}" .format(resp.text))
            data = resp.json()

            """ GPT Style Response from vLLM server
              {"id":"cmpl-8282910626ff42518fb0e17f01c412f7",
              "object":"text_completion","created":1798628,"model":"meta-llama/Llama-2-7b-chat-hf",
                     "choices":[{"index":0,"text":
            """
            d = data["choices"]
            t = d[0]
            res = t["text"]
            res = {"generated_text" : res}
            #print("LLAMA2 JSON Response: {0}" .format(res))

            content, is_code = self.get_content(res)
            #content, is_code = self.get_content(data[0])
            content = content.replace(prmpt, "")
            if content and taskid:
                self.publish_to_redis(content, taskid)
            return (content), is_code
            
        except Exception as e:
            #print('error calling llama2: {0}' .format(str(e)))
            print('LLAMA2 failed as {}'.format(e))
            return None, None
            
