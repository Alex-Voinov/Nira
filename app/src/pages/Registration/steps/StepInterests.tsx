import type { FormData } from "@/types/FormData";

const INTERESTS = ["Спорт", "Музыка", "Книги", "Путешествия", "Игры", "Кино"];

type Props = {
  data: FormData;
  setData: (data: FormData) => void;
};

export default function StepInterests({ data, setData }: Props) {
  const toggleInterest = (interest: string) => {
    if (data.interests.includes(interest)) {
      setData({ ...data, interests: data.interests.filter(i => i !== interest) });
    } else {
      setData({ ...data, interests: [...data.interests, interest] });
    }
  };

  return (
    <div className="step">
      <h2>Интересы</h2>
      <div className="interests">
        {INTERESTS.map(i => (
          <button
            key={i}
            className={data.interests.includes(i) ? "interest selected" : "interest"}
            onClick={() => toggleInterest(i)}
          >
            {i}
          </button>
        ))}
      </div>
    </div>
  );
}
