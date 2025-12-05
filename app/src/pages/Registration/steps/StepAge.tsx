import type { FormData } from "@/types/FormData";

type Props = {
  data: FormData;
  setData: (data: FormData) => void;
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
