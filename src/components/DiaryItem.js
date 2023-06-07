import { useNavigate } from "react-router-dom";
import MyButton from "./MyButton";

const DiaryItem = ({ id, emotion, title, content, created_at }) => {
  const strDate = new Date(created_at).toLocaleString();

  const navigate = useNavigate();

  const goDetail = () => {
    navigate(`/diary/${id}`);
  };

  return (
    <div className="DiaryItem">
      <div
        onClick={goDetail}
        className={[
          "emotion_img_wrapper",
          `emotion_img_wrapper_${emotion}`,
        ].join(" ")}
      >
        <img src={process.env.PUBLIC_URL + `assets/emotion${emotion}.png`} />
      </div>
      <div className="info_wrapper" onClick={goDetail}>
        <div className="diary_date">{strDate}</div>
        <div className="diray_content_prview">{content.slice(0, 25)}</div>
      </div>
      <div className="btn_wrapper flex items-center"></div>
    </div>
  );
};

export default DiaryItem;
