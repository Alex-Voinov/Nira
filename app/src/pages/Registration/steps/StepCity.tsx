import { useState, useEffect, type FC } from "react";
import type { IStep } from "../RegistrationPage";

type NominatimItem = {
  address: {
    city?: string;
    town?: string;
    village?: string;
  };
};

const fallbackCities = [
  "London",
  "Manchester",
  "Birmingham",
  "Liverpool",
  "Leeds",
  "Glasgow",
  "Edinburgh",
  "Bristol",
  "Nottingham",
  "Sheffield",
];

const StepCity: FC<IStep> = ({ data, setData }) => {
  const [query, setQuery] = useState("");
  const [cities, setCities] = useState<string[]>([]);
  const [notInUk, setNotInUk] = useState(false); // ← чекбокс

  useEffect(() => {
    if (notInUk) {
      setCities([]);
      return; // если чекбокс активен, ничего не ищем
    }

    if (query.length < 2) {
      setCities([]);
      return;
    }

    let cancelled = false;

    async function fetchCities() {
      try {
        const url = `https://nominatim.openstreetmap.org/search?format=json&addressdetails=1&country=United%20Kingdom&city=${encodeURIComponent(
          query
        )}`;

        const res = await fetch(url, {
          headers: {
            "Accept-Language": "en",
            "User-Agent": "NiraApp/1.0",
          },
        });

        if (!res.ok) throw new Error("API error");

        const json: NominatimItem[] = await res.json();
        if (cancelled) return;

        const names = json
          .map(
            (item) =>
              item.address.city ||
              item.address.town ||
              item.address.village
          )
          .filter(Boolean) as string[];

        const unique = Array.from(new Set(names));

        if (unique.length === 0) {
          const filtered = fallbackCities.filter((c) =>
            c.toLowerCase().includes(query.toLowerCase())
          );
          setCities(filtered);
        } else {
          setCities(unique);
        }
      } catch {
        if (!cancelled) {
          const filtered = fallbackCities.filter((c) =>
            c.toLowerCase().includes(query.toLowerCase())
          );
          setCities(filtered);
        }
      }
    }

    const debounce = setTimeout(fetchCities, 300);

    return () => {
      cancelled = true;
      clearTimeout(debounce);
    };
  }, [query, notInUk]);

  return (
    <div className="step">
      <h2>Город</h2>

      <input
        type="text"
        value={query}
        onChange={(e) => {
          setQuery(e.target.value);
          setData({ ...data, city: e.target.value });
        }}
        placeholder="Город"
        className="input"
        disabled={notInUk} // ← блокировка
      />

      {/* чекбокс */}
      <label style={{ marginTop: "8px", display: "flex", gap: "8px" }}>
        <input
          type="checkbox"
          checked={notInUk}
          onChange={(e) => {
            const checked = e.target.checked;
            setNotInUk(checked);

            if (checked) {
              setQuery("");
              setCities([]);
              setData({ ...data, city: "" }); // очищаем город
            }
          }}
        />
        Живу не в UK
      </label>

      {!notInUk && cities.length > 0 && (
        <div className="autocomplete">
          {cities.map((city) => (
            <div
              key={city}
              className="option"
              onClick={() => {
                setQuery(city);
                setData({ ...data, city });
              }}
            >
              {city}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}


export default StepCity;