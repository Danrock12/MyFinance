import { redirect } from '@sveltejs/kit';

export function load() {
  throw redirect(302, `/financial-report/${new Date().getFullYear()}`);
}

export const prerender = true;