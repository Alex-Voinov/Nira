import type { IUser } from "@/types/user";
import type { Dispatch, SetStateAction } from "react";

type Props = {
  data: IUser;
  setData: (data: IUser) => void;
  setActiveNextStep: Dispatch<SetStateAction<boolean>>;
};

export default function StepAge({ data, setData }: Props) {
  return (
    <div className="step">
      <h2>Сколько тебе лет?</h2>
      <input
        type="number"
        min={16}
        value={data.age < 0 ? 16 : data.age}
        onChange={(e) => setData({ ...data, age: Number(e.target.value) })}
        placeholder="Возраст"
      />
    </div>
  );
}
