import type { IUser } from "@/types/user";
import type { Dispatch, FC, SetStateAction } from "react";

type Props = {
  data: IUser;
  setData: (data: IUser) => void;
  setActiveNextStep: Dispatch<SetStateAction<boolean>>;
};

const StepGender: FC<Props> = ({ data, setData }) => {
  const options = [
    { value: "male", label: "Мужской" },
    { value: "female", label: "Женский" },
    { value: "other", label: "Другое" },
  ] as const;

  return (
    <div className="step">
      <h2>Твой гендер</h2>

      <div className="radio-group">
        {options.map((opt) => (
          <label key={opt.value}>
            <input
              type="radio"
              name="gender"
              value={opt.value}
              checked={data.gender === opt.value}
              onChange={() =>
                setData({ ...data, gender: opt.value })
              }
            />
            {opt.label}
          </label>
        ))}
      </div>
    </div>
  );
};

export default StepGender;
