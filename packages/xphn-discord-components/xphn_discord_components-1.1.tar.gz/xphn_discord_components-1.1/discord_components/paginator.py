
from .component import Button, ButtonStyle

class Paginator:
    def __init__(self, bot, ctx, embed, items_per_page=10, inline=False):
        self.bot = bot
        self.ctx = ctx
        self.embed = embed
        self.items_per_page = items_per_page
        self.current_page = 0
        self.pages = []
        self.page_embed = None
        self.inline = inline
        
    def create_pages(self, fields):
        """Split embed fields into multiple pages."""
        for i in range(0, len(fields), self.items_per_page):
            page = fields[i:i + self.items_per_page]
            self.pages.append(page)

    async def send_initial_message(self):
        """Send the first page of the embed with buttons."""
        self.update_embed_page()
        self.page_embed = await self.ctx.send(
            embed=self.embed,
            components=[
                [
                    Button(emoji="◀️", custom_id="paginator_prev", style=ButtonStyle.blue),
                    Button(emoji="▶️", custom_id="paginator_next", style=ButtonStyle.blue),
                ]
            ]
        )

        # Wait for button click and handle it
        while True:
            try:
                res = await self.bot.wait_for("button_click", timeout=30.0, check=lambda i: i.custom_id.startswith("paginator"))
                await self.handle_click(res)
            except TimeoutError:
                # Handle timeout, disable buttons
                await self.page_embed.edit(components=[])
                break

    def update_embed_page(self):
        """Update the embed to show only the current page of fields."""
        self.embed.clear_fields()
        for field in self.pages[self.current_page]:
            self.embed.add_field(name=field['name'], value=field['value'], inline=self.inline)
        self.embed.set_footer(text=f"Page {self.current_page + 1}/{len(self.pages)}")

    async def handle_click(self, res):
        """Handle button click response."""
        if res.component.custom_id == 'paginator_prev':
            self.current_page = max(0, self.current_page - 1)
        elif res.component.custom_id == 'paginator_next':
            self.current_page = min(len(self.pages) - 1, self.current_page + 1)

        self.update_embed_page()
        await res.respond(type=7, embed=self.embed)  # Edit the original message with the new page



