import { useState } from "react";
import { useNavigate } from "react-router-dom";

import DiaryItem from "./DiaryItem";
import MyButton from "./MyButton";

const sortOptionList = [
  { value: "latest", name: "최신순" },
  { value: "oldest", name: "오래된 순" },
];

const filterOptionList = [
  { value: "all", name: "전체" },
  { value: "sad", name: "슬픔" },
  { value: "happy", name: "기쁨" },
  { value: "angry", name: "분노" },
  { value: "anxiety", name: "불안" },
  { value: "surprise", name: "놀람" },
];

const ControlMenu = ({ value, onChange, optionList }) => {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="ControlMenu"
    >
      {optionList.map((it, idx) => (
        <option value={it.value} key={idx}>
          {it.name}
        </option>
      ))}
    </select>
  );
};

const DiaryList = ({ diaryList }) => {
  const navigate = useNavigate();

  const [sortType, setSortType] = useState("latest");
  const [filter, setFilter] = useState("all");

  const getProcessedDiaryList = () => {
    const filterCallBack = (item) => {
      console.log(item, filter);
      if (filter === "sad") {
        return item.emotion == "슬픔";
      } else if (filter === "happy") {
        return item.emotion == "기쁨";
      } else if (filter === "angry") {
        return item.emotion == "분노";
      } else if (filter === "anxiety") {
        return item.emotion == "불안";
      } else if (filter === "surprise") {
        return item.emotion == "놀람";
      }
    };

    const compare = (a, b) => {
      if (sortType === "all") {
        return parseInt(b.date) - parseInt(a.date);
      } else {
        return parseInt(a.date) - parseInt(b.date);
      }
    };

    const copyList = JSON.parse(JSON.stringify(diaryList));

    const filteredList =
      filter === "all" ? copyList : copyList.filter((it) => filterCallBack(it));
    const sortedList = filteredList.sort(compare);
    return sortedList;
  };

  return (
    <div className="DiaryList">
      <div className="memu_wrapper">
        <div className="left_col">
          <ControlMenu
            value={sortType}
            onChange={setSortType}
            optionList={sortOptionList}
          />
          <ControlMenu
            value={filter}
            onChange={setFilter}
            optionList={filterOptionList}
          />
        </div>
        <div className="right_col h-full rounded-lg">
          <MyButton
            type={"positive"}
            text={"새 일기쓰기"}
            className="bg-teal-700 rounded-lg h-full py-2 text-black"
            onClick={() => navigate("/New")}
          />
        </div>
      </div>
      {getProcessedDiaryList().map((it) => (
        <DiaryItem key={it.id} {...it} />
      ))}
    </div>
  );
};

DiaryList.defaultProps = {
  diaryList: [],
};

export default DiaryList;
