const MyButton = ({ text, type, onClick }) => {
  // btnType 설정 이유 
  // props로 받는 type안에 'positive or negativ가 있는지 확인하고 없다면 type을 default로 강제시킨다
  // includes : 배열이 특정 요소를 포함하고 있는지 판별하는 매서드
  const btnType = ['positive', 'negative'].includes(type) ? type : 'default'  
    
  return (
    <button onClick={onClick} className={['MyButton', `MyButton_${btnType}`].join(" ")}>
      {text}
    </button>
  );
};

MyButton.defaultProps = {
    type: 'default'
}

export default MyButton;

