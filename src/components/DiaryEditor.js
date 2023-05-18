import MyHearder from "./MyHearder";
import MyButton from "./MyButton";

import { useNavigate } from "react-router-dom";
import { useContext, useRef, useState } from "react";
import { DiaryDispatchContext } from "./../App.js";

import EmotionItem from "./EmotionItem";
import { createClient } from "@supabase/supabase-js";
import { auth } from "../firebase-config";

const supabase = createClient(
  "https://rivtwrqbjelldspdcgew.supabase.co",
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJpdnR3cnFiamVsbGRzcGRjZ2V3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODQxODc3MjQsImV4cCI6MTk5OTc2MzcyNH0.km6nIGYqTJfCGmknERU2gVIdt-kpXrIIey5YYm-ixiE"
);

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

// const getStringDate = (date) => {
//   return date.toISOString().slice(0, 10);
//   // toISOString 메서드는 단순화한 확장 ISO형식의 문자열은 반환한다
//   // YYYY-MM-DDTHH로 표현한다
// };
const getStringDate = (date) => {
  let year = date.getFullYear();

  let month = date.getMonth() + 1;

  let day = date.getDate();

  if (month < 10) {
    month = `0${month}`;
  }

  if (day < 10) {
    day = `0${day}`;
  }
  return `${year}-${month}-${day}`;
};

const DiaryEditor = ({ isEdit, originData }) => {
  const contentRef = useRef();
  const titleRef = useRef();

  const [date, setDate] = useState(getStringDate(new Date()));
  const [emotion, setEmotion] = useState(3);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");

  const { onCreate } = useContext(DiaryDispatchContext);

  const handleClickEmotion = (emotion) => {
    setEmotion(emotion);
  };

  const navigate = useNavigate();

  const handleSubmit = async () => {
    if (content.length < 1) {
      contentRef.current.focus();
      return;
    }
    if (
      window.confirm(
        isEdit ? "일기를 수정하시겠습니까?" : "새로운 일기를 작성하시겠습니까?"
      )
    ) {
      if (!isEdit) {
        onCreate(date, content, emotion);
      } else {
        // onEdit(originData.id, date, content, emotion);
      }
    }
    const email = auth.currentUser.email;
    await supabase.from("diary").insert({ title, content, emotion, email });
    navigate("/Home", { replace: true });
  };

  return (
    <div className="DiaryEditor w-full">
      <MyHearder
        headText={"새 일기쓰기"}
        leftChild={
          <MyButton text={"< 뒤로가기"} onClick={() => navigate(-1)} />
        }
      />
      <div>
        <section>
          <h4>오늘은 언제인가요?</h4>
          <div className="input_box">
            <input
              className="input_date"
              type="date"
              value={date || ""}
              // React input 관련 오류 => input의 value에 undefined가 들어갔을 경우에 대한 처리가 없음.
              // input의 value가 undefined 일 때 ""가 들어올 수 있게 해준다
              onChange={(e) => setDate(e.target.value)}
            />
          </div>
        </section>
        <section>
          <h4>오늘의 감정</h4>
          <div className="input_box emotion_list_wrapper">
            {emotionList.map((it) => (
              <EmotionItem
                key={it.emotion_id}
                onClick={handleClickEmotion}
                isSelected={it.emotion_description === emotion}
                {...it}
              />
            ))}
          </div>
        </section>
        <section>
          <h4>오늘의 일기</h4>
          <div className="input_box_text_wrapper">
            <input
              placeholder="제목"
              ref={titleRef}
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
          </div>
          <div className="input_box_text_wrapper">
            <textarea
              placeholder="오늘은 어땠나요"
              ref={contentRef}
              value={content}
              onChange={(e) => setContent(e.target.value)}
            />
          </div>
        </section>
        <section>
          <div className="control_box flex flex-col">
            <MyButton
              text={"감정분석하기"}
              className="bg-teal-700 hover:bg-teal-800 transition-colors text-white rounded-lg py-2 px-4 w-full mb-2"
              onClick={() => {
                navigate("/Emotion ");
              }}
            />
            <MyButton
              text={"작성하기"}
              type={"positive"}
              className="bg-emerald-500 hover:bg-emerald-600 transition-colors text-white rounded-lg py-2 px-4 w-full"
              onClick={handleSubmit}
            />
          </div>
        </section>
      </div>
    </div>
  );
};

export default DiaryEditor;
