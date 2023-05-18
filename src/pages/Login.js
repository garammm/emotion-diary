import { useState } from "react";
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  onAuthStateChanged,
  signOut,
} from "firebase/auth";
import { auth } from "../firebase-config";
import MyButton from "../components/MyButton";
import { useNavigate } from "react-router-dom";
import styled from "@emotion/styled";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

export default function Login() {
  const [registerEmail, setRegisterEmail] = useState("");
  const [registerPassword, setRegisterPassword] = useState("");
  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");
  const [user, setUser] = useState({});

  //   onAuthStateChanged(auth, (currentUser) => {
  //     setUser(currentUser);
  //   });
  const navigate = useNavigate();
  const register = async () => {
    try {
      const user = await createUserWithEmailAndPassword(
        auth,
        registerEmail,
        registerPassword
      );
      console.log(user);
    } catch (error) {
      console.log(error.message);
    }
  };

  const login = async () => {
    try {
      const user = await signInWithEmailAndPassword(
        auth,
        loginEmail,
        loginPassword
      );
      navigate("/Home");

      console.log(user);
    } catch (error) {
      console.log(error.message);
      toast("이메일과 비밀번호를 다시 확인해주세요");
    }
  };

  const logout = async () => {
    await signOut(auth);
  };

  return (
    <Container className="shadow-lg rounded-xl p-8 w-96 m-auto">
      <div className="w-full">
        <h3 className="text-2xl font-bold mb-2">당신의 감정은, 어떠신가요?</h3>
        <h3 className="text-xl font-bold mb-4 text-gray-500">
          감정 다이어리 시작하기
        </h3>
        <Label className="text-lg font-bold">아이디</Label>
        <input
          className="w-full outline-none border-b border-gray-300"
          placeholder="이메일을 입력해주세요"
          onChange={(event) => {
            setLoginEmail(event.target.value);
          }}
        />
        <br></br>
        <br></br>
        <Label>비밀번호</Label>
        <input
          className="w-full outline-none border-b border-gray-300"
          type="password"
          placeholder="비밀번호를 입력해주세요"
          onChange={(event) => {
            setLoginPassword(event.target.value);
          }}
        />
      </div>
      <br></br>
      <MyButton
        text="로그인"
        className="text-xs w-full py-2 rounded-lg bg-green-300 hover:bg-green-500 transition-colors mb-2"
        onClick={login}
      />
      {user?.email}
      <MyButton
        text={"아직 회원이 아니신가요?"}
        className="text-xs w-full py-2 rounded-lg bg-gray-100 hover:bg-gray-200 transition-colors mb-2"
        onClick={() => navigate("/SignUp")}
      />
      {user?.email}
      <ToastContainer
        position="bottom-center"
        type="success"
        autoClose={3000}
      />
      {/* <MyButton
        className="text-xs w-full py-2 rounded-lg bg-green-300 hover:bg-green-500 transition-colors"
        text={"로그아웃"}
        onClick={logout}
      /> */}
    </Container>
  );
}

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const Label = styled.label`
  font-sie: 13px;
  display: block;
  color: #999;
  margin-bottom: 4px;
`;
