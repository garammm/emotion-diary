const EmotionItem = ({
  emotion_id,
  emotion_img,
  emotion_description,
  onClick,
  className,
  isSelected,
}) => {
  return (
    <div
      onClick={() => onClick(emotion_description)}
      className={[
        "EmotionItem",
        className,
        isSelected ? `EmotionItem_on_${emotion_id}` : `EmotionItem_off`,
      ].join(" ")}
    >
      <img src={emotion_img} />
      <span>{emotion_description}</span>
    </div>
  );
};

export default EmotionItem;
