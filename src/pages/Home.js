import React, { useContext, useEffect, useState } from "react";
import MyHeader from "../components/MyHearder";
import MyButton from "../components/MyButton";
import DiaryList from "../components/DiaryList";
import { createClient } from "@supabase/supabase-js";
import { auth } from "../firebase-config";

const supabase = createClient(
  "https://rivtwrqbjelldspdcgew.supabase.co",
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJpdnR3cnFiamVsbGRzcGRjZ2V3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODQxODc3MjQsImV4cCI6MTk5OTc2MzcyNH0.km6nIGYqTJfCGmknERU2gVIdt-kpXrIIey5YYm-ixiE"
);

const Home = () => {
  const [data, setData] = useState([]);
  const [curDate, setCurDate] = useState(new Date());
  const [diaryList, setDiaryList] = useState([]);
  const headText = `${curDate.getFullYear()}년 ${curDate.getMonth() + 1}월`;

  const fetchDiaryList = async () => {
    const { data } = await supabase
      .from("diary")
      .select()
      .filter("email", "eq", auth.currentUser?.email);
    setDiaryList(data);
  };

  useEffect(() => {
    auth.onAuthStateChanged(() => fetchDiaryList());
  }, []);

  // 그 달의 일기를 보여주는 함수
  useEffect(() => {
    if (diaryList?.length >= 1) {
      const firstDay = new Date(
        curDate.getFullYear(),
        curDate.getMonth(),
        1
      ).getTime();

      const lastDay = new Date(
        curDate.getFullYear(),
        curDate.getMonth() + 1,
        0
      ).getTime();

      setData(
        diaryList?.filter((it) => firstDay <= it.date && it.date <= lastDay)
      );
    }
  }, [diaryList, curDate]);

  const increaseMonth = () => {
    setCurDate(
      new Date(curDate.getFullYear(), curDate.getMonth() + 1, curDate.getDate())
    );
  };

  const decreaseMonth = () => {
    setCurDate(
      new Date(curDate.getFullYear(), curDate.getMonth() - 1, curDate.getDate())
    );
  };

  return (
    <div className="w-full">
      <MyHeader
        headText={headText}
        leftChild={<MyButton text={"<"} onClick={decreaseMonth} />}
        rightChild={<MyButton text={">"} onClick={increaseMonth} />}
      />
      <DiaryList diaryList={diaryList} />
    </div>
  );
};

export default Home;
