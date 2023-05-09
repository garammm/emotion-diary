import { useParams } from "react-router-dom";
 

const Diary = () => {
    const {id} = useParams();

    console.log(id)
    return (
        <div>
            <h1>Diary</h1>
            <div>상세 페이지</div>
        </div>
    )
}

export default Diary;
