from __future__ import annotations

import enum
import os
from dataclasses import dataclass
from pathlib import Path
from typing import AsyncIterable, ClassVar, Iterable

import aiofiles
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Input, Static


def main() -> None:
    tty_fd = 0
    t24_fd = os.dup(tty_fd)
    with Path("/dev/tty").open() as tty:
        os.dup2(tty.fileno(), tty_fd)

    ViewerApp(t24_fd).run(inline=True)


@dataclass
class Page:
    header: PacketX
    g0_set: str
    g1_set: str
    lines: dict[int, PacketX]


class ViewerApp(App):
    BINDINGS: ClassVar = [
        Binding("down", "navigate_relative(+1)", "Next page"),
        Binding("up", "navigate_relative(-1)", "Previous page"),
        Binding("pageup", "navigate_relative(-100)", "Previous magazine"),
        Binding("pagedown", "navigate_relative(+100)", "Next magazine"),
        Binding("home", 'navigate_absolute("100")', "Go home", priority=True),
    ]

    def __init__(self, t42_fd: int) -> None:
        super().__init__(ansi_color=True)

        self.t42_fd = t42_fd
        self.pages = {}
        self.line_fields = []

    def compose(self) -> ComposeResult:
        input_field = Input("100", max_length=3, type="integer")
        self.input_field = input_field
        yield input_field

        header = Static()
        self.header = header
        yield header

        for _ in range(25):
            line_field = Static(" " * 40)
            self.line_fields.append(line_field)
            yield line_field

    def on_mount(self) -> None:
        self.input_field.styles.border = "none"
        self.input_field.styles.height = 1
        self.input_field.styles.padding = 0
        self.run_worker(self.read_t42())

    def on_input_changed(self, event: Input.Changed) -> None:
        page = self.pages.get(event.value)
        if page is None:
            return

        self.render_data(page, self.header, page.header.data[8:])
        for line_number, packet in page.lines.items():
            self.render_data(page, self.line_fields[line_number], packet.data)
        self.end_of_page(page)

    def action_navigate_relative(self, offset: int) -> None:
        page_number = int(self.input_field.value) + offset
        page_number_min = 100
        page_number_max = 999
        if page_number < page_number_min:
            page_number = page_number_max
        elif page_number > page_number_max:
            page_number = page_number_min
        self.action_navigate_absolute(str(page_number))

    def action_navigate_absolute(self, page_number: str) -> None:
        self.input_field.value = page_number

    async def read_t42(self) -> None:
        async for packet in parse_packets(self.t42_fd):
            match packet:
                case PacketX(packet_number, page_number, data):
                    match packet_number:
                        case 0:
                            g0_set = LATIN_SET
                            g1_set = MOSAICS_SET[:0x20] + g0_set[0x20:0x40] + MOSAICS_SET[0x20:]
                            page = Page(packet, g0_set, g1_set, {})
                            self.pages[page_number] = page
                            if page_number == self.input_field.value:
                                self.render_data(page, self.header, data[8:])
                        case 26 | 27 | 28:
                            continue
                        case _:
                            page = self.pages[page_number]
                            line_number = packet_number - 1
                            page.lines[line_number] = packet
                            if page_number == self.input_field.value:
                                self.render_data(page, self.line_fields[line_number], data)
                case EndOfPage(page_number):
                    page = self.pages[page_number]
                    if page_number == self.input_field.value:
                        self.end_of_page(page)

    def end_of_page(self, page: Page) -> None:
        # Clear lines that we have not received
        for i in range(25):
            if i not in page.lines:
                self.render_data(page, self.line_fields[i], b" " * 40)

    def render_data(self, page: Page, field: Static, data: bytes) -> None:
        data = decode_odd_parity(data)
        text = "".join(parse_chars(page, data))
        field.update(text)


def decode_8_4(byte: int) -> int:
    d1 = byte >> 1 & 0b1
    d2 = byte >> 3 & 0b1
    d3 = byte >> 5 & 0b1
    d4 = byte >> 7 & 0b1
    return (d1 << 0) | (d2 << 1) | (d3 << 2) | (d4 << 3)


def decode_odd_parity(bs: bytes) -> bytes:
    return b"".join((byte & 0x7F).to_bytes() for byte in bs)


@dataclass
class Packet:
    packet_number: int


@dataclass
class PacketX(Packet):
    page_number: str
    data: bytes


@dataclass
class EndOfPage:
    page_number: str


async def parse_packets(fd: int) -> AsyncIterable[Packet | EndOfPage]:
    current_page_numbers: dict[int, str] = {}

    async with aiofiles.open(fd, "rb") as reader:
        while packet := await reader.read(42):
            byte1 = decode_8_4(packet[0])
            byte2 = decode_8_4(packet[1])
            data = packet[2:]
            magazine = byte1 & 0b111
            packet_number = (byte2 << 1) | (byte1 >> 3)

            match packet_number:
                case 0:
                    page_number = current_page_numbers.get(magazine)
                    if page_number is not None:
                        yield EndOfPage(page_number)

                    page_number_units = decode_8_4(data[0])
                    page_number_tens = decode_8_4(data[1])
                    page_number = f"{magazine}{page_number_tens:x}{page_number_units:x}"
                    current_page_numbers[magazine] = page_number
                    yield PacketX(packet_number, page_number, data)
                case 29 | 30 | 31:
                    pass
                case _:
                    page_number = current_page_numbers.get(magazine)
                    if page_number is not None:
                        yield PacketX(packet_number, page_number, data)


LATIN_SET = " !\"#¬%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~■"
LATIN_ENGLISH_SET = "£$@←½→↑#―¼‖¾÷"
LATIN_FRENCH_SET = "éïàëêùî#èâôûç"
MOSAICS_SET = " 🬀🬁🬂🬃🬄🬅🬆🬇🬈🬉🬊🬋🬌🬍🬎🬏🬐🬑🬒🬓▌🬔🬕🬖🬗🬘🬙🬚🬛🬜🬝🬞🬟🬠🬡🬢🬣🬤🬥🬦🬧▐🬨🬩🬪🬫🬬🬭🬮🬯🬰🬱🬲🬳🬴🬵🬶🬷🬸🬹🬺🬻█"


COLORS = (
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
)


class CharacterSize(enum.Enum):
    NORMAL = 0x0C
    DOUBLE_HEIGHT = 0x0D
    DOUBLE_WIDTH = 0x0E
    DOUBLE_SIZE = 0x0F


@dataclass
class Attributes:
    foreground: str = "white"
    mosaic: bool = False
    size: CharacterSize = CharacterSize.NORMAL
    box: bool = False
    switch: bool = False
    separated_mosaics: bool = False
    hold_mosaics: bool = False
    held_mosaic: str = " "
    conceal: bool = False


def parse_chars(page: Page, data: bytes) -> Iterable[str]:  # noqa: C901, PLR0912, PLR0915
    attr = Attributes()

    for byte in data:
        match byte:
            case 0x00 | 0x01 | 0x02 | 0x03 | 0x04 | 0x05 | 0x06 | 0x07:
                color = COLORS[byte - 0x00]
                if attr.mosaic:
                    attr.held_mosaic = " "
                attr.mosaic = False
                attr.foreground = color
                attr.conceal = False
                yield f"[{color}]"
            case 0x08:
                yield "[blink]"
            case 0x09:
                yield "[/blink]"
            case 0x0A:
                attr.box = False
            case 0x0B:
                attr.box = True
            case 0x0C | 0x0D | 0x0E | 0x0F:
                size_new = CharacterSize(byte)
                if attr.size != size_new:
                    attr.held_mosaic = " "
                attr.size = size_new
            case 0x10 | 0x11 | 0x12 | 0x13 | 0x14 | 0x15 | 0x16 | 0x17:
                color = COLORS[byte - 0x10]
                if not attr.mosaic:
                    attr.held_mosaic = " "
                attr.mosaic = True
                attr.foreground = color
                attr.conceal = False
                yield f"[{color}]"
            case 0x18:
                attr.conceal = True
            case 0x19:
                attr.separated_mosaics = False
            case 0x1A:
                attr.separated_mosaics = True
            case 0x1B:
                attr.switch = not attr.switch
            case 0x1C:
                yield "[on black]"
            case 0x1D:
                yield f"[on {attr.foreground}]"
            case 0x1E:
                attr.hold_mosaics = True
            case 0x1F:
                attr.hold_mosaics = False
            case _:
                char_set = page.g1_set if attr.mosaic else page.g0_set
                char = char_set[byte - 0x20]
                if byte & 0b0010_0000:
                    attr.held_mosaic = char
                yield char
                continue
        yield attr.held_mosaic if attr.hold_mosaics else " "


if __name__ == "__main__":
    main()
