import gsap from "gsap";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const Emotion = () => {
  const navigate = useNavigate();

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

  return (
    <div className="flex flex-col items-center justify-center w-full">
      <div
        className="font-bold text-gray-700 text-2xl mb-3"
        id="감정분석_결과_1"
      >
        오늘은 위로가 필요한 날이군요?
      </div>
      <div
        className="font-bold text-gray-700 text-2xl mb-12"
        id="감정분석_결과_2"
      >
        당신의 감정은 ______ 입니다.
      </div>
      <button
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
      </button>
    </div>
  );
};

export default Emotion;
