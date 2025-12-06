import type { FormData } from "@/types/FormData";
import type { FC } from "react";

type Props = {
  data: FormData;
  setData: (data: FormData) => void;
};

const StepShowGender: FC<Props> = ({ data, setData }) => {
  const options = [
    { value: "male", label: "Только мужчин" },
    { value: "female", label: "Только женщин" },
    { value: "mix", label: "Всех (микс)" },
  ] as const;

  return (
    <div className="step">
      <h2>Кого показывать в рекомендациях?</h2>

      <div className="options">
        {options.map((opt) => (
          <label key={opt.value}>
            <input
              type="radio"
              name="showGender"
              value={opt.value}
              checked={data.showGender === opt.value}
              onChange={() => setData({ ...data, showGender: opt.value })}
            />
            {opt.label}
          </label>
        ))}
      </div>
    </div>
  );
}

export default StepShowGender
