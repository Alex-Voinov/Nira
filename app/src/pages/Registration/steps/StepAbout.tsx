import type { IUser } from "@/types/user";
import type { Dispatch, SetStateAction } from "react";

type Props = {
  data: IUser;
  setData: (data: IUser) => void;
  setActiveNextStep: Dispatch<SetStateAction<boolean>>;
};

export default function StepAbout({ data, setData }: Props) {
  return (
    <div className="step">
      <h2>О себе</h2>
      <textarea
        value={data.description || ''}
        onChange={(e) => setData({ ...data, description: e.target.value })}
        placeholder="Расскажи немного о себе"
        className="textarea"
        rows={4}
      />
    </div>
  );
}
