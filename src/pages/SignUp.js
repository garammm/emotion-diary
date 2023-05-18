import DiarySignUp from "../components/DiarySignUp";
import MyButton from "../components/MyButton";
import { useNavigate } from "react-router-dom";

const SignUp = () => {
  const navigate = useNavigate();

  return (
    <div className="rounded-xl shadow-lg p-8">
      <DiarySignUp />
      <MyButton
        text={"로그인 하러 가기"}
        onClick={() => navigate("/")}
        className="text-center mt-2 text-xs w-full hover:bg-slate-300 rounded-xl transition-colors py-2 px-4"
      />
    </div>
  );
};

export default SignUp;
