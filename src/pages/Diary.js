import { createClient } from "@supabase/supabase-js";
import { useState } from "react";
import { useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { emotionList } from "../components/DiaryEditor";

const supabase = createClient(
  "https://rivtwrqbjelldspdcgew.supabase.co",
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJpdnR3cnFiamVsbGRzcGRjZ2V3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODQxODc3MjQsImV4cCI6MTk5OTc2MzcyNH0.km6nIGYqTJfCGmknERU2gVIdt-kpXrIIey5YYm-ixiE"
);

const Diary = () => {
  const { id } = useParams();
  const [diary, setDiary] = useState();
  const navigate = useNavigate();

  const getDiaryContent = async () => {
    const { data } = await supabase.from("diary").select().eq("id", id);
    setDiary(() => data[0]);
  };

  const editDiary = async () => {
    await supabase
      .from("diary")
      .update({ ...diary })
      .eq("id", id);
  };

  const editTitle = () => {};

  useEffect(() => {
    getDiaryContent();
  }, []);

  return diary ? (
    <div className="px-4 py-8 w-full">
      <img
        className="mx-auto mb-4 w-30 h-30"
        src={
          emotionList?.find(
            (emotion) => emotion?.emotion_description === diary.emotion
          )?.emotion_img
        }
      />
      <h1 className="text-2xl font-bold mb-2">{diary?.title}</h1>
      <div className="p-4 border border-gray-200 rounded-xl mb-4 whitespace-pre-line">
        {diary?.content}
      </div>
      <button
        onClick={() => navigate(-1)}
        class="w-full rounded-lg py-2 px-4 bg-teal-800 hover:bg-teal-800 transition-colors text-white font-semibold"
      >
        목록으로 돌아가기
      </button>
    </div>
  ) : (
    <div>일기를 불러오고 있어요...</div>
  );
};

export default Diary;
