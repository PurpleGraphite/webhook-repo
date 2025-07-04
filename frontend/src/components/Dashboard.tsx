import { useEffect, useRef, useState } from 'react';
import EventCard from './EventCard';

type GitActivityEvent = {
	_id: string;
	request_id: string;
	author: string;
	action: 'PUSH' | 'PULL_REQUEST' | 'MERGE';
	from_branch: string | null;
	to_branch: string;
	timestamp: string;
};

function Dashboard() {
	const [events, setEvents] = useState<GitActivityEvent[]>([]);
	const latestTimestampRef = useRef<string | null>(null);

	async function pollData() {
		try {
			const url = latestTimestampRef.current
				? `http://localhost:5000/poll-events?latest-timestamp=${encodeURIComponent(
						latestTimestampRef.current
				  )}`
				: `http://localhost:5000/poll-events`;

			const res = await fetch(url);
			if (!res.ok) throw new Error('Failed to fetch events');

			const newEvents: GitActivityEvent[] = await res.json();

			if (newEvents.length > 0) {
				const latestTimestamp =
					newEvents[newEvents.length - 1].timestamp;
				if (latestTimestamp)
					latestTimestampRef.current = latestTimestamp;

				setEvents((prev) => [...prev, ...newEvents]);
			}
		} catch (err) {
			console.error('Polling error:', err);
		}
	}

	useEffect(() => {
		pollData();
		const interval = setInterval(() => {
			pollData();
		}, 15000);

		return () => clearInterval(interval);
	}, []);

	return (
		<>
			<div className="h-full w-fit border-2 py-4 px-12 rounded border-slate-600 border-dashed ">
				<h3 className="text-left mb-4">All Events</h3>
				<div className="h-11/12 w-full overflow-y-scroll">
					<div className="flex flex-col gap-4">
						{events
							.slice()
							.reverse()
							.map((elem, idx) => (
								<EventCard
									key={idx + 1}
									type={elem.action}
									author={elem.author}
									fromBranch={elem.from_branch}
									toBranch={elem.to_branch}
									timestamp={elem.timestamp}
								></EventCard>
							))}
					</div>
				</div>
			</div>
		</>
	);
}

export default Dashboard;
