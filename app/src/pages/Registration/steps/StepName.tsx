import type { IUser } from "@/types/user";

type Props = {
  data: IUser;
  setData: (data: IUser) => void;
};

export default function StepName({ data, setData }: Props) {
  return (
    <div className="step">
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
