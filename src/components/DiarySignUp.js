import { useState } from "react";
import { createUserWithEmailAndPassword } from "firebase/auth";
import { auth } from "../firebase-config";
import { useNavigate } from "react-router-dom";

const Diary_sign_up = () => {
  const [registerEmail, setRegisterEmail] = useState("");
  const [registerPassword, setRegisterPassword] = useState("");
  const navigate = useNavigate();

  const register = async () => {
    try {
      const user = await createUserWithEmailAndPassword(
        auth,
        registerEmail,
        registerPassword
      );
      navigate("/Home");
    } catch (error) {
      console.log(error.message);
    }
  };

  return (
    <div className="flex flex-col w-72">
      <h3 className="text-xl font-bold mb-2 text-gray-700">회원 가입</h3>
      <div className="mb-1">이메일</div>
      <input
        className="w-full outline-none border-b border-gray-300"
        placeholder="이메일을 입력하세요"
        onChange={(event) => {
          setRegisterEmail(event.target.value);
        }}
      />
      <br></br>
      <div className="mb-1">비밀번호</div>
      <input
        className="w-full outline-none border-b border-gray-300"
        placeholder="비밀번호를 입력하세요"
        onChange={(event) => {
          setRegisterPassword(event.target.value);
        }}
      />
      <button
        onClick={register}
        className="bg-emerald-300 hover:bg-emerald-500  transition-colors rounded-xl py-2 px-4 text-xs mt-4"
      >
        감정 다이어리 시작하기
      </button>
    </div>
  );
};

export default Diary_sign_up;
