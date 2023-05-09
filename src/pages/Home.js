import React, { useContext, useEffect, useState } from "react";

import MyHeader from "../components/MyHearder";
import MyButton from "../components/MyButton";
import DiaryList from "../components/DiaryList";

import { DiaryStateContext } from "../App";
import axios from "axios";

const Home = () => {
  // const diaryList = useContext(DiaryStateContext);

  //   console.log(diaryList)
  const [data, setData] = useState([]);
  const [curDate, setCurDate] = useState(new Date());
  const [diaryList, setDiaryList] = useState([]);

  const headText = `${curDate.getFullYear()}년 ${curDate.getMonth() + 1}월`;

  const fetchDiaryList = async () => {
    const data = await axios(
      "https://sn5yv5fku8.execute-api.ap-northeast-2.amazonaws.com/dev/"
    );

    console.log(data);
    setDiaryList(() => data);
  };

  useEffect(() => {
    fetchDiaryList();
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
      // const lastDay = new Date(
      //   curDate.getFullYear(),
      //   curDate.getMonth() + 1,
      //   0
      // ).getTime();

      // setData(
      //   diaryList.filter((it) => firstDay <= it.date && it.date < lastDay)
      // );
    }
  }, [diaryList, curDate]);

  // useEffect(() => {
  //   console.log(data);
  // }, [data]);

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
    <div>
      <MyHeader
        headText={headText}
        leftChild={<MyButton text={"<"} onClick={decreaseMonth} />}
        rightChild={<MyButton text={">"} onClick={increaseMonth} />}
      />
      <DiaryList diaryList={diaryList.data} />
    </div>
  );
};

export default Home;
