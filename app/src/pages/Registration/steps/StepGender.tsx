import type { FormData } from "@/types/FormData";

type Props = {
  data: FormData;
  setData: (data: FormData) => void;
};

export default function StepGender({ data, setData }: Props) {
  return (
    <div className="step">
      <h2>Твой гендер</h2>
      <div className="radio-group">
        {["male", "female", "other"].map((g) => (
          <label key={g}>
            <input
              type="radio"
              name="gender"
              value={g}
              checked={data.gender === g}
              onChange={() => setData({ ...data, gender: g as any })}
            />
            {g === "male" ? "Мужской" : g === "female" ? "Женский" : "Другое"}
          </label>
        ))}
      </div>
    </div>
  );
}
