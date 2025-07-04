import convertTimestamp from '../utils/convertTimestamp';

type EventCardProps = {
	type: 'PUSH' | 'PULL_REQUEST' | 'MERGE';
	author: string;
	fromBranch: string | null;
	toBranch: string;
	timestamp: string;
};

function EventCard({
	type,
	author,
	fromBranch,
	toBranch,
	timestamp,
}: EventCardProps) {
	const convertedTimestamp = convertTimestamp(timestamp);
	return (
		<div className="font-nunito max-w-xl min-w-xl py-4 px-4 bg-gray-200 w-fit rounded text-sm">
			<div className="flex gap-2">
				<h4 className={`text-[#DC143C] font-semibold`}>
					{type}:
				</h4>
				{type === 'PUSH' ? (
					<p>
						{`"${author}" pushed to "${toBranch}" on ${convertedTimestamp}`}
					</p>
				) : type === 'PULL_REQUEST' ? (
					<p>{`"${author}" submitted a pull request from "${fromBranch}" to "${toBranch}" ${convertedTimestamp}`}</p>
				) : type === 'MERGE' ? (
					<p>{`"${author}" merged branch "${fromBranch}" to "${toBranch}" on ${convertedTimestamp}`}</p>
				) : null}
			</div>
		</div>
	);
}
export default EventCard;
