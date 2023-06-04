import gsap from "gsap";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import EmotionItem from "../components/EmotionItem";

export const emotionList = [
  {
    emotion_id: 1,
    emotion_img: process.env.PUBLIC_URL + `/assets/emotion슬픔.png`,
    emotion_description: "슬픔",
  },
  {
    emotion_id: 2,
    emotion_img: process.env.PUBLIC_URL + `/assets/emotion기쁨.png`,
    emotion_description: "기쁨",
  },
  {
    emotion_id: 3,
    emotion_img: process.env.PUBLIC_URL + `/assets/emotion분노.png`,
    emotion_description: "분노",
  },
  {
    emotion_id: 4,
    emotion_img: process.env.PUBLIC_URL + `/assets/emotion불안.png`,
    emotion_description: "불안",
  },
  {
    emotion_id: 5,
    emotion_img: process.env.PUBLIC_URL + `/assets/emotion놀람.png`,
    emotion_description: "놀람",
  },
];

const Emotion = () => {
  const navigate = useNavigate();
  const [emotion, setEmotion] = useState(3);
  const handleClickEmotion = (emotion) => {
    setEmotion(emotion);
  };

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
      <div id="step-2-container" className="hidden">
        <div className="flex flex-col items-center justify-center text-center">
          <div className="font-bold text-gray-700 text-2xl mb-3">
            감정 분석이 완료되었어요.
          </div>
          <section>
            <h4 className="text-lg font-bold mb-4">오늘의 감정은...</h4>
            <div className="flex space-x-4 input_box emotion_list_wrapper">
              {emotionList.map((it) => (
                <EmotionItem
                  className="min-w-[100px]"
                  key={it.emotion_id}
                  onClick={handleClickEmotion}
                  isSelected={it.emotion_description === emotion}
                  {...it}
                />
              ))}
            </div>
          </section>
        </div>
      </div>
      {/* <button
        onClick={() => navigate("/New")}
        className="py-2 px-4 rounded-lg bg-teal-500 text-white mb-2"
        id="감정분석_결과_3"
      >
        이어서 작성하기
      </button>
      <button
        onClick={() => navigate("/Home")}
        className="py-2 px-4 rounded-lg bg-teal-700 text-white"
        id="감정분석_결과_3"
      >
        목록으로 돌아가기
      </button> */}
    </div>
  );
};

export default Emotion;
