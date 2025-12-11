import type { FC } from "react";
import type { IStep } from "../RegistrationPage";
import styles from './gender.module.css'


const StepShowGender: FC<IStep> = ({ data, setData }) => {
  const options = [
    { value: "male", label: "Только мужчины" },
    { value: "female", label: "Только женщины" },
    { value: "mix", label: "Все (микс)" },
  ] as const;

  return (
    <div>
      <h2>Кто интересен?</h2>
      <div className={styles.selectorsBlock}>
        {options.map(opt => (
          <label key={opt.value} className={styles.option}>
            <input
              type="radio"
              name="gender"
              value={opt.value}
              checked={data.show_gender === opt.value}
              onChange={() => setData({ ...data, show_gender: opt.value })}
            />
            <span className={styles.labelText}>{opt.label}</span>
          </label>
        ))}
      </div>
    </div>
  );
}

export default StepShowGender
