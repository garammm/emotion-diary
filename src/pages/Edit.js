import { useNavigate, useSearchParams } from "react-router-dom";

const Edit = () => {
  const navigate = useNavigate();

  const [serachParams, setSearchParams] = useSearchParams();

  const id = serachParams.get("id");
  // console.log(id)
  const mode = serachParams.get("mode");
  // console.log(mode)

  return (
    <div>
      <h1>Edit</h1>
      <div>일기 수정페이지</div>
      <button onClick={() => setSearchParams({ who: "유가람" })}>바꾸기</button>
      <button
        onClick={() => {
          navigate("/Home");
        }}
      >
        Home으로 가기
      </button>
      <button
        onClick={() => {
          navigate(-1); // -1은 뒤로가기
        }}
      >
        뒤로가기
      </button>
    </div>
  );
};

export default Edit;
