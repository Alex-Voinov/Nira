import type { IUser } from "@/types/user";
import type { Dispatch, FC, SetStateAction } from "react";

const INTERESTS = ["Спорт", "Музыка", "Книги", "Путешествия", "Игры", "Кино"];

interface IStepInterests {
  data: IUser;
  setData: (data: IUser) => void;
  setActiveNextStep: Dispatch<SetStateAction<boolean>>;
};

const StepInterests: FC<IStepInterests> = ({ data, setData }) => {
  const toggleInterest = (interest: string) => {
    if (data.goal.includes(interest)) {
      setData({ ...data, goal: data.goal.filter(i => i !== interest) });
    } else {
      setData({ ...data, goal: [...data.goal, interest] });
    }
  };

  return (
    <div className="step">
      <h2>Интересы</h2>
      <div className="interests">
        {INTERESTS.map(i => (
          <button
            key={i}
            type="button"
            className={data.goal.includes(i) ? "interest selected" : "interest"}
            onClick={() => toggleInterest(i)}
          >
            {i}
          </button>
        ))}
      </div>
    </div>
  );
}

export default StepInterests
