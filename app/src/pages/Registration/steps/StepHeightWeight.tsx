import type { FormData } from "@/types/FormData";

type Props = {
  data: FormData;
  setData: (data: FormData) => void;
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
