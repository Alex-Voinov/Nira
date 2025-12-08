import type { IUser } from "@/types/user";

type Props = {
  data: IUser;
  setData: (data: IUser) => void;
};

export default function StepHeightWeight({ data, setData }: Props) {
  return (
    <div className="step">
      <h2>Рост и вес</h2>
      <input
        type="number"
        placeholder="Рост (см)"
        value={data.height ?? ""}
        onChange={(e) => setData({ ...data, height: Number(e.target.value) })}
        className="input"
      />
      <input
        type="number"
        placeholder="Вес (кг)"
        value={data.weight ?? ""}
        onChange={(e) => setData({ ...data, weight: Number(e.target.value) })}
        className="input"
      />
    </div>
  );
}
