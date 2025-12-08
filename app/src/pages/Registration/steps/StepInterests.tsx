import type { IUser } from "@/types/user";

const INTERESTS = ["Спорт", "Музыка", "Книги", "Путешествия", "Игры", "Кино"];

type Props = {
  data: IUser;
  setData: (data: IUser) => void;
};

export default function StepInterests({ data, setData }: Props) {
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
