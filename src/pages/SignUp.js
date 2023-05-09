import DiarySignUp from "../components/DiarySignUp";
import MyButton from "../components/MyButton";
import { useNavigate } from "react-router-dom";

const SignUp = () => {
  const navigate = useNavigate();

  return (
    <div>
      <DiarySignUp />
      <MyButton text={"로그인 하러 가기"} onClick={() => navigate("/")} />
    </div>
  );
};

export default SignUp;
