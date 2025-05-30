<script>

    import '../app.css'
	let { children } = $props();

    let location = $state('/')
    function change_location(loc){
        location = loc;
        console.log(location)
    }

    //Icons
    import { House } from '@lucide/svelte';
    let pages = [
        {'name': 'Home', 'url': '/', 'icon': House}
    ]

</script>


<main class="  bg-teal-700 overflow-clip h-screen max-w-screen">
    <div class="bg-zinc-100 drop-shadow-lg w-full h-12">

    </div>
    <section class="grid grid-cols-[auto_1fr] w-screen min-h-[calc(100vh-3rem)] h-fit">
        <aside class="w-[150px] m-4">
            <nav class="py-4">
                <div class="w-[300px] mb-6 grid grid-cols-[auto_1fr] place-content-[start_center]">
                    <!-- <House color='#f1f5f9' /> -->
                    <h1 class="text-slate-100 text-2xl font-bold">AI Skribent</h1>
                </div>
                <ul>
                    <li class="w-[150px]">
                        {#each pages as page}
                        <a  onclick={() => change_location(page.url)} 
                            class="{location === page.url ? 'bg-slate-100' : 'bg-none text-slate-100'} hover:bg-slate-300 hover:text-slate-700 grid grid-cols-[auto_1fr] place-content-center gap-3 mb-4 pl-4 py-1 rounded-xl text-md" 
                            href={page.url}>
                            <page.icon class="w-4 h-4 m-auto mt-1" />
                            <button class="w-full cursor-pointer text-left">
                                {page.name}
                            </button>
                        </a>
                        {/each}
                    </li>
                </ul>
            </nav>
        </aside>
    
        <aside class="bg-zinc-100 p-8 mx-6 mb-4 mt-4 rounded-2xl">
            {@render children()}
        </aside>
    </section>
</main>