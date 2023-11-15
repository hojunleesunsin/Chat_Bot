import re

class Text_Classification:
    def __init__(self, text, Sub):
        self.text = text
        self.Sub = Sub

    def Time_Pattern(self):
        if "오전" in self.text:
            return "오전"
        elif "오후" in self.text:
            return "오후"
        elif "하루" in self.text:
            return "하루"
    def Date_Pattern(self):
      # 연도를 option으로 사용하며 월,일만을 입력해도 인지 가능
        date_pattern = r"\b(?:\d{4}년\s*)?\d{1,2}월\s+\d{1,2}일\b"
        date_matches = re.findall(date_pattern, self.text)
        date = date_matches[0] if date_matches else None
        return date

    def Address_Pattern(self):
        # 한국의 주소 특성상 법적으로 옳바른 주소가 많지 않기 떄문에 시/군/구 와 로/길/대로 또는 동/읍/면을 이용하였으며
        # 그 뒤 숫자가 포함되는 형식을 채택하였습니다.
        # 이외에도 특이한 형태의 주소가 존재하기 떄문에 이후 추가 예정
        if re.search(r"(로|길|대로) \d+(?:-\d+)?", self.text):
            address_pattern = r"\b[\w\s-]+(?:시|군|구) [\w\s-]+(?:로|길|대로) \d+(?:-\d+)?"
        else:
            address_pattern = r"\b[\w\s-]+(?:시|군|구) [\w\s-]+(?:동|읍|면) \d+(?:-\d+)?"

        address_matches = re.findall(address_pattern, self.text)
        address = address_matches[0] if address_matches else None
        return address

    def Pay_Pattern(self):
        # (,)를 option으로 사용하며 원으로 끝나는 Text를 Pay로 인지하도록 작성
        pay_pattern = r"\b\d+(?:,\d+)*원\b"
        pay_matches = re.findall(pay_pattern, self.text)
        pay = pay_matches[0] if pay_matches else None
        return pay

    def Sub_TF(self):
        # 기타 내용을 따로 작성하며 이는 존재 여부만 파악하여 추출합니다.
        if self.Sub is None:
            Sub = "Sub is None"
        else:
            Sub = self.Sub
        return Sub

def text_classifier(text, sub):
    classifier = Text_Classification(text, sub)

    time = classifier.Time_Pattern()
    date = classifier.Date_Pattern()
    address = classifier.Address_Pattern()
    pay = classifier.Pay_Pattern()
    Sub_text = classifier.Sub_TF()

    print("Time", time)
    print("Date:", date)
    print("Address:", address)
    print("Pay:", pay)
    print("Sub:", Sub_text)