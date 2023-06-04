import gsap from "gsap";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import EmotionItem from "../components/EmotionItem";

export const emotionList = [
  {
    emotion_id: 1,
    emotion_img: process.env.PUBLIC_URL + `/assets/emotion슬픔.png`,
    emotion_description: "슬픔",
    emotion_content:
      "뭔가 슬픈 일이 있으셨나 보네요.\n너무 좌절하지 말고, 금방 에너지를 회복할 수 있을 거에요.",
  },
  {
    emotion_id: 2,
    emotion_img: process.env.PUBLIC_URL + `/assets/emotion기쁨.png`,
    emotion_description: "기쁨",
    emotion_content:
      "오늘은 기쁜 하루였군요!.\n오늘의 긍정적인 에너지를 잃지 않길 바래요.",
  },
  {
    emotion_id: 3,
    emotion_img: process.env.PUBLIC_URL + `/assets/emotion분노.png`,
    emotion_description: "분노",
    emotion_content:
      "잘 안 풀리는 일이 있었나요?\n금방 털어낸 뒤, 다시 활력을 되찾길 바래요.",
  },
  {
    emotion_id: 4,
    emotion_img: process.env.PUBLIC_URL + `/assets/emotion불안.png`,
    emotion_description: "불안",
    emotion_content:
      "컨디션이 좋지 않은 상황인가요?\n조금 휴식을 취한 뒤, 평안을 되찾을 수 있도록 해보세요.",
  },
  {
    emotion_id: 5,
    emotion_img: process.env.PUBLIC_URL + `/assets/emotion놀람.png`,
    emotion_description: "놀람",
    emotion_content:
      "놀라운 일이 있었군요!\n새로운 일이 닥치더라도, 즐겁게 받아들일 수 있길 바래요.",
  },
];

const 슬픔_키워드 = ["슬", "슬픔", "슬픈 날", "슬픈", "우울", "아쉽", "이런"];
const 기쁨_키워드 = [
  "기쁨",
  "좋",
  "행복",
  "뿌듯",
  "보람",
  "친구",
  "만남",
  "설렘",
];
const 분노_키워드 = ["분노", "화", "나쁜", "억울", "짜증", "애매"];
const 불안_키워드 = [
  "떨린",
  "두렵",
  "기다",
  "불안",
  "오들",
  "두근",
  "무서운",
  "무서",
];
const 놀람_키워드 = ["놀람", "깜짝", "황급", "화들짝", "어이쿠"];

const Emotion = ({ updateEmotion, content, closeEmotion }) => {
  const navigate = useNavigate();
  const [emotion, setEmotion] = useState(3);
  const [emotionContent, setEmotionContent] = useState("");

  useEffect(() => {
    if (
      슬픔_키워드.find((keyword) => {
        return content.includes(keyword);
      })
    ) {
      setEmotion("슬픔");
    } else if (
      기쁨_키워드.find((keyword) => {
        return content.includes(keyword);
      })
    ) {
      setEmotion("기쁨");
    } else if (
      분노_키워드.find((keyword) => {
        return content.includes(keyword);
      })
    ) {
      setEmotion("분노");
    } else if (
      불안_키워드.find((keyword) => {
        return content.includes(keyword);
      })
    ) {
      setEmotion("불안");
    } else if (
      놀람_키워드.find((keyword) => {
        return content.includes(keyword);
      })
    ) {
      setEmotion("놀람");
    } else {
      const targetIndex = Math.floor(Math.random() * 100) % 5;
      setEmotion(() => emotionList[targetIndex]?.emotion_description);
    }
  }, [content]);

  useEffect(() => {
    const emotionIndex = emotionList.findIndex(
      (item) => item.emotion_description === emotion
    );
    setEmotionContent(() => emotionList[emotionIndex]?.emotion_content);
    updateEmotion(() => emotion);
  }, [emotion]);

  useEffect(() => {
    const emotionContainer1 = document.getElementById("감정분석_결과_1");
    const emotionContainer2 = document.getElementById("감정분석_결과_2");
    const emotionContainer3 = document.querySelectorAll("감정분석_결과_3");
    const timeline = gsap.timeline();
    timeline
      .fromTo(
        emotionContainer1,
        {
          opacity: 0,
          y: 100,
        },
        {
          opacity: 1,
          y: 0,
          duration: 0.75,
        }
      )
      .fromTo(
        emotionContainer2,
        {
          opacity: 0,
          y: 100,
        },
        {
          opacity: 1,
          y: 0,
          duration: 0.75,
        }
      )
      .fromTo(
        emotionContainer3,
        {
          opacity: 0,
          y: 100,
        },
        {
          opacity: 1,
          y: 0,
          duration: 0.75,
        }
      );
  }, []);

  useEffect(() => {
    setTimeout(() => {
      const timeline = gsap.timeline();
      timeline
        .to("#step-1-container", {
          opacity: 0,
        })
        .to("#step-1-container", {
          display: "none",
        })
        .to("#step-2-container", {
          display: "block",
        })
        .to("#step-2-container", {
          opacity: 1,
        });
      // alert("dd");
    }, 0);
  }, []);

  return (
    <div className="fixed top-0 left-0 w-full h-screen flex flex-col items-center justify-center bg-white">
      <div className="flex flex-col items-center justify-center w-full">
        <div
          id="step-1-container"
          className="flex flex-col items-center justify-center"
        >
          <div
            className="font-bold text-gray-700 text-2xl mb-3"
            id="감정분석_결과_1"
          >
            일기 내용을 기반으로 감정을 분석할게요.
          </div>
          <div
            className="font-bold text-gray-700 text-2xl mb-8"
            id="감정분석_결과_2"
          >
            약 10초 정도 시간이 소요될 수 있어요.
          </div>
          <img src="/loading.svg" alt="로딩 중" className="w-24 h-24 mb-8" />
        </div>
        <div id="step-2-container" className="hidden opacity-0">
          <div className="flex flex-col items-center justify-center text-center">
            <div className="font-bold text-gray-700 text-2xl mb-3">
              감정 분석이 완료되었어요.
            </div>
            <section className="mb-2">
              <h4 className="text-lg font-bold mb-4">오늘의 감정은...</h4>
              <div className="flex space-x-4 input_box emotion_list_wrapper">
                {emotionList.map((it) => (
                  <EmotionItem
                    className={`min-w-[200px] min-h-[240px] ${
                      it.emotion_description !== emotion ? "hidden" : "flex"
                    }`}
                    key={it.emotion_id}
                    isSelected={it.emotion_description === emotion}
                    {...it}
                  />
                ))}
              </div>
            </section>
            <div className="whitespace-pre-line mb-8 text-sm text-gray-700">
              {emotionContent}
            </div>
          </div>
          <div className="flex flex-col items-center space-y-4 mx-auto">
            <button
              onClick={() => closeEmotion()}
              className="py-2 px-4 rounded-lg bg-teal-500 text-white w-40"
              id="감정분석_결과_3"
            >
              이어서 작성하기
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Emotion;
