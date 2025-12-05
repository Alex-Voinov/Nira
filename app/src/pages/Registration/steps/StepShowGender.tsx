import type { FormData } from "@/types/FormData";

type Props = {
  data: FormData;
  setData: (data: FormData) => void;
};

export default function StepShowGender({ data, setData }: Props) {
  return (
    <div className="step">
      <h2>Показывать гендер в профиле?</h2>
      <label>
        <input
          type="checkbox"
          checked={data.showGender}
          onChange={(e) => setData({ ...data, showGender: e.target.checked })}
        />
        Да, показывать
      </label>
    </div>
  );
}
