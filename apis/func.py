import os
import openai
from summa.summarizer import summarize



class chatgpt_func():
    def __init__(self, open_ai_key):

        openai.api_key = open_ai_key
        self.abstract_template = """Input: {input}
        Output: abstract input as 3 line
        """
        
        self.translate_template = """Input: {input}
        Output: 모든 Input을 한국어로 번역해주세요
        """

    def preprocess(self, text):

        self.summarized_text = text
        ratio = 0.5
        self.summarized_text = summarize(self.summarized_text, ratio=ratio)

        while len(self.summarized_text) > 1900:
            ratio -= 0.01
            self.summarized_text = summarize(text, ratio=ratio)

        self.summarized_text = self.summarized_text.replace('.', '. \n')

        return self.summarized_text, ratio
        
    def translate_func(self, text):

        print('입력 : '+self.summarized_text)
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": self.translate_template},
                {"role": "user", "content": self.summarized_text},
            ]
        )
        return response['choices'][0]['message']['content']

if __name__ == "__main__":
    lang = chatgpt_func()
    input = 'This paper presents a flash LiDAR sensor featuring an in-pixel histogramming time-to-digital converter (hTDC) based on a delta-intensity quaternary search (DIQS) technique. The proposed 12-b DIQS hTDC is a two-step converter consisting of a 6-b coarse hTDC and a 7-b fine hTDC with 1-b redundancy. The DIQS hTDC synthesizes depth maps with three subframes from the coarse mode and a single subframe from the fine mode, achieving 100-ps resolution without a clock frequency of a few GHz. The DIQS repeats dividing the time range of a current step into four periods and finding the location where a target object is placed by comparing the number of events in each period, which is similar to the binary search method but doubles its operating speed. Two time-of-flight (ToF) bits are consecutively determined in every coarse step, and seven ToF bits are estimated by the indirect ToF technique with photon counts. An up-down counter is employed to reduce the memory size by half and enable the delta-intensity technique that can extend the dynamic range by suppressing the uniform background light. The prototype LiDAR with an 80×60 pixel array was fabricated in a 110-nm CIS process and fully characterized. The maximum detectable range is measured to 45 m with a success rate of 100% at night and 60% under 70-klux background light. The depth accuracy and precision are 2.5 cm and 1.5 cm from 3 m to 4.5 m indoor, respectively, and the precision is maintained to 1.8 cm for the target located at a 1.5-m distance under 60-klux background light. Inherent time-gating and differential signaling of the DIQS hTDC effectively suppress common-mode noise, accomplishing real-time acquisition of depth images with 30 fps in a 9-m range at 30-klux background light.'
    print(lang.preprocess(input))