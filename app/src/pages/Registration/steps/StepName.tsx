import type { IUser } from "@/types/user";
import type { Dispatch, SetStateAction } from "react";

type Props = {
  data: IUser;
  setData: (data: IUser) => void;
  setActiveNextStep: Dispatch<SetStateAction<boolean>>;
};

export default function StepName({ data, setData, setActiveNextStep }: Props) {
  setActiveNextStep(data.name.length > 3)
  return (
    <div>
      <h2>Как тебя зовут?</h2>
      <input
        type="text"
        value={data.name}
        onChange={(e) => setData({ ...data, name: e.target.value })}
        placeholder="Имя"
        className="input"
      />
    </div>
  );
}
