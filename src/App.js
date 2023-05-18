import React, { useReducer, useRef } from "react";
import "./App.css";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import New from "./pages/New";
import Edit from "./pages/Edit";
import Diary from "./pages/Diary";
import Login from "./pages/Login";
import Emotion from "./pages/Emotion";
import sign_up from "./pages/SignUp";
import SignUp from "./pages/SignUp";
import { auth } from "./firebase-config";

const reducer = (state, action) => {
  let newState = [];
  switch (action.type) {
    case "INIT": {
      return action.data;
    }
    case "CREATE": {
      newState = [action.data, ...state];
      break;
    }
    case "REMOVE": {
      newState = state.filter((it) => it.id !== action.targetId);
      break;
    }
    case "EDIT": {
      newState = state.map((it) =>
        it.id === action.data.id ? { ...action.data } : it
      );
      break;
    }
    default:
      return state;
  }
  return newState;
};

export const DiaryStateContext = React.createContext();
export const DiaryDispatchContext = React.createContext();

const dummyData = [
  /*
  {
    id: 1,
    emotion: 1,
    content: "오늘의 일기",
    date: 1681879773893,
  },

  {
    id: 2,
    emotion: 2,
    content: "오늘의 일기2",
    date: 1681879773894,
  },
  {
    id: 3,
    emotion: 3,
    content: "오늘의 일기3",
    date: 1681879773895,
  },
  {
    id: 4,
    emotion: 4,
    content: "오늘의 일기4",
    date: 1681879773896,
  },
  {
    id: 5,
    emotion: 5,
    content: "오늘의 일기5",
    date: 1681879773897,
  },*/
];

function App() {
  const [data, dispatch] = useReducer(reducer, dummyData);
  const dataId = useRef(0);
  // 추가
  const onCreate = (date, content, emotion) => {
    dispatch({
      type: "CREATE",
      data: {
        id: dataId.current,
        date: new Date(date).getTime(),
        content,
        emotion,
      },
    });
    dataId.current += 1;
  };

  // 삭제
  const onRemove = (targetId) => {
    dispatch({ type: "REMOVE", targetId });
  };

  // 수정
  const onEdit = (targetId, date, content, emotion) => {
    dispatch({
      type: "EDIT",
      data: {
        id: targetId,
        date: new Date(date).getTime(),
        content,
        emotion,
      },
    });
  };

  return (
    <DiaryStateContext.Provider value={data}>
      <DiaryDispatchContext.Provider
        value={{
          onCreate,
          onEdit,
          onRemove,
        }}
      >
        <BrowserRouter>
          <div className="App flex">
            <Routes>
              <Route path="/Home" element={<Home />}></Route>
              <Route path="/new" element={<New />}></Route>
              <Route path="/edit/:id" element={<Edit />} />
              <Route path="/diary/:id" element={<Diary />}></Route>
              <Route
                path="/"
                element={
                  <div className="flex h-full m-auto justify-center items-center">
                    <Login />
                  </div>
                }
              ></Route>
              <Route
                path="/signUp"
                element={
                  <div className="flex h-full m-auto justify-center items-center">
                    <SignUp />
                  </div>
                }
              ></Route>
              <Route path="/Emotion" element={<Emotion />}></Route>
            </Routes>
          </div>
        </BrowserRouter>
      </DiaryDispatchContext.Provider>
    </DiaryStateContext.Provider>
  );
}

export default App;

//<img src={process.env.PUBLIC_URL + `/assets/emotion1.png`} alt="" />가 작동을 하지 않는다면 이렇게 설정해서 사용할 수 있음
// const env = process.env;
// env.PUBLIC_URL = env.PUBLIC_URL || "";
