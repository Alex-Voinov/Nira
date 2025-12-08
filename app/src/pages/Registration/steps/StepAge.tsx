import type { IUser } from "@/types/user";

type Props = {
  data: IUser;
  setData: (data: IUser) => void;
};

export default function StepAge({ data, setData }: Props) {
  return (
    <div className="step">
      <h2>Сколько тебе лет?</h2>
      <input
        type="number"
        min={13}
        value={data.age ?? ""}
        onChange={(e) => setData({ ...data, age: Number(e.target.value) })}
        placeholder="Возраст"
        className="input"
      />
    </div>
  );
}
