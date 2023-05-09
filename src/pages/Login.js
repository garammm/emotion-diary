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
    }
  };

  const logout = async () => {
    await signOut(auth);
  };

  return (
    <Container>
      <div>
        <h3> 로그인</h3>
        <Label>아이디</Label>
        <input
          placeholder="Email..."
          onChange={(event) => {
            setLoginEmail(event.target.value);
          }}
        />
        <br></br>
        <br></br>
        <Label>비번</Label>
        <input
          placeholder="Password..."
          onChange={(event) => {
            setLoginPassword(event.target.value);
          }}
        />
      </div>
      <br></br>
      <MyButton text="로그인" onClick={login} />

      <h3> 회원가입 </h3>
      {user?.email}
      <MyButton text={"회원가입"} onClick={() => navigate("/SignUp")} />
      <h3> 로그 아웃 </h3>
      {user?.email}
      <MyButton text={"로그아웃"} onClick={logout} />
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
