<script lang="ts">
	import * as Card from '$lib/components/ui/card/index.js';
	import { Textarea } from '$lib/components/ui/textarea/index.js';
	import { buttonVariants } from '$lib/components/ui/button';
	import { Badge } from '$lib/components/ui/badge/index.js';
	import { voices, type UserRequestType } from '$lib/types/apiTypes';
	import { type VoiceType, type PromptType, UserRequest } from '$lib/types/apiTypes';

	let { handleSubmit } = $props<{
		handleSubmit: (userRequest: UserRequestType) => void;
	}>();

	let voice = $state<VoiceType | undefined>();
	let prompt = $state<PromptType>('');
	let error = $state('');

	const submitForm = () => {
		const result = UserRequest.safeParse({ voice, prompt });
		if (!result.success) {
			if (result.error.issues[0].code == 'too_small') {
				error = 'Prompt too short!';
			} else {
				error = 'Voice not selected!';
			}
		} else {
			handleSubmit({ voice, prompt });
		}
	};
</script>

<div class="flex h-screen w-full flex-col items-center gap-4">
	<Card.Root class="w-2/3">
		<Card.Header>
			<Card.Title>Enter Prompt</Card.Title>
			<Card.Description>Describe what the video should explain</Card.Description>
		</Card.Header>
		<Card.Content>
			<form class="flex flex-col items-start" onsubmit={submitForm}>
				<Textarea class="mb-4" name="prompt" placeholder="Enter video idea" bind:value={prompt} />

				<input type="hidden" name="voice" bind:value={voice} />

				<div class="flex w-full justify-between">
					<div class="flex gap-2">
						{#each voices as voiceOption}
							<Badge class="h-6" variant={voice === voiceOption ? 'default' : 'outline'}>
								<label>
									<input
										class="sr-only"
										type="radio"
										name="scoops"
										value={voiceOption}
										bind:group={voice}
									/>
									{voiceOption.charAt(0).toLocaleUpperCase() + voiceOption.slice(1)}
								</label>
							</Badge>
						{/each}
					</div>
					<button class="w-20 {buttonVariants({ variant: 'default' })}">Submit</button>
				</div>
			</form>
			{#if error}
				<div>{error}</div>
			{/if}
		</Card.Content>
	</Card.Root>
</div>
