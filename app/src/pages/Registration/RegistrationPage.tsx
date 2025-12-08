import { useState, useEffect } from "react";
import StepName from "./steps/StepName";
import StepAge from "./steps/StepAge";
import StepGender from "./steps/StepGender";
import StepShowGender from "./steps/StepShowGender";
import StepCity from "./steps/StepCity";
import StepHeightWeight from "./steps/StepHeightWeight";
import StepInterests from "./steps/StepInterests";
import StepAbout from "./steps/StepAbout";
import StepSummary from "./steps/StepSummary";
import styles from "./RegistrationPage.module.css";
import { formInitialState, type FormData } from "@/types/user";


export default function RegistrationPage() {
  const [step, setStep] = useState(0);
  const [tgId, setTgId] = useState<number | null>(null);

  const [data, setData] = useState<FormData>(formInitialState);

  // Получаем tg_id через Telegram Web App
  useEffect(() => {
    // @ts-ignore
    if (window.Telegram?.WebApp?.initDataUnsafe) {
      // @ts-ignore
      setTgId(Number(window.Telegram.WebApp.initDataUnsafe.user?.id));
    }
  }, []);

  useEffect(() => {
    if (tgId) setData((prev) => ({ ...prev, tg_id: tgId }));
  }, [tgId]);

  const steps = [
    <StepName data={data} setData={setData} />,
    <StepAge data={data} setData={setData} />,
    <StepGender data={data} setData={setData} />,
    <StepShowGender data={data} setData={setData} />,
    <StepCity data={data} setData={setData} />,
    <StepHeightWeight data={data} setData={setData} />,
    <StepInterests data={data} setData={setData} />,
    <StepAbout data={data} setData={setData} />,
    <StepSummary data={data} />,
  ];

  const progress = Math.round(((step + 1) / steps.length) * 100);

  return (
    <div className={styles.container}>
      <div className={styles.progressBar}>
        <div className={styles.progress} style={{ width: `${progress}%` }} />
      </div>
      {steps[step]}
      <button onClick={() => setStep(step - 1)} style={{ marginTop: "16px" }}>
        Назад
      </button>
      <button onClick={() => setStep(step + 1)} style={{ marginTop: "16px" }}>
        Далее
      </button>
    </div>
  );
}
