export interface Health {
  status: string;
  version: string;
  dev_mode: boolean;
}

export async function getHealth(): Promise<Health> {
  const response = await fetch("/api/health");
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}
