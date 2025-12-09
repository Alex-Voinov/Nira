import type { IUser } from "@/types/user";
import type { Dispatch, FC, SetStateAction } from "react";

type Props = {
  data: IUser;
  setData: (data: IUser) => void;
  setActiveNextStep: Dispatch<SetStateAction<boolean>>;
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
