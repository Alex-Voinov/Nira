import type { FC } from "react";
import type { IStep } from "../RegistrationPage";


const StepShowGender: FC<IStep> = ({ data, setData }) => {
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
              checked={data.show_gender === opt.value}
              onChange={() => setData({ ...data, show_gender: opt.value })}
            />
            {opt.label}
          </label>
        ))}
      </div>
    </div>
  );
}

export default StepShowGender
