class CustomDataService {
  constructor() {
    this.sentimentAnalysisPublisher = this.$sentimentAnalysis;
    this.sentimentAnalysis = null;
    this.cancellables = new Set();
  }

  fetchSentimentAnalysis(text) {
    const urlRequest = this.getURLRequest(text);
    if (!urlRequest) {
      return;
    }
    fetch(urlRequest)
      .then((response) => response.json())
      .then((returnedData) => {
        this.sentimentAnalysis = returnedData;
      })
      .catch((error) => {
        console.log(error);
      });
  }

  getURL() {
    const urlString = CustomAPI.sentiment.urlString;
    try {
      const url = new URL(urlString);
      return url;
    } catch (error) {
      console.log(error);
      return null;
    }
  }

  getURLRequest(body) {
    const url = this.getURL();
    if (!url) {
      return null;
    }
    const headers = new Headers();
    headers.append(
      CustomAPI.sentiment.clientHeaderContentType,
      CustomAPI.sentiment.clientContent
    );
    const urlRequest = new Request(url, {
      method: "POST",
      headers: headers,
      body: JSON.stringify({ content: body }),
    });
    return urlRequest;
  }

  handleOutput(output) {
    if (!(output instanceof Response) || output.status !== 200) {
      throw new Error("Bad server response");
    }
    return output.json();
  }
}

const CustomAPI = {
  sentiment: {
    clientHeaderContentType: "Content-Type",
    clientContent: "application/json",
    urlString: "[YOUR RETURNED NGROK URL]",
  },
};

class SentimentModel {
  constructor(label, document, sentences) {
    this.label = label;
    this.document = document;
    this.sentences = sentences;
  }

  get labelString() {
    if (!this.label) {
      return "";
    }
    switch (this.label) {
      case "0":
        return "불안";
      case "1":
        return "놀람";
      case "2":
        return "분노";
      case "3":
        return "슬픔";
      case "4":
        return "분노";
      case "5":
        return "가쁨";
      default:
        return "";
    }
  }

  get labelImageString() {
    if (!this.label) {
      return "";
    }
    switch (this.label) {
      case "0":
        return process.env.PUBLIC_URL + `/assets/emotion불안.png`;
      case "1":
        return process.env.PUBLIC_URL + `/assets/emotion놀람.png`;
      case "2":
        return process.env.PUBLIC_URL + `/assets/emotion분노.png`;
      case "3":
        return process.env.PUBLIC_URL + `/assets/emotion슬픔.png`;
      case "4":
        return process.env.PUBLIC_URL + `/assets/emotion분노.png`;
      case "5":
        return process.env.PUBLIC_URL + `/assets/emotion기쁨.png`;
      default:
        return "";
    }
  }
}

if (viewModel.sentimentAnalysis) {
  if (viewModel.sentimentAnalysis.document) {
    const sentimentText = document.sentiment;
    // Implement UI logic to display sentimentText as a headline with the desired view modifier
  }

  const labelImageString = viewModel.sentimentAnalysis.labelImageString;
  // Implement UI logic to display the image based on labelImageString

  const labelString = viewModel.sentimentAnalysis.labelString;
  // Implement UI logic to display labelString as a headline
}
