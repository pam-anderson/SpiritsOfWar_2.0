library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity gpio_com is
port (
    clk: in std_logic;
    reset_n: in std_logic;
    addr: in std_logic_vector(1 downto 0);
    rd_en: in std_logic;
    wr_en: in std_logic;
    readdata: out std_logic_vector(31 downto 0);
    writedata: in std_logic_vector(31 downto 0);
	 serialdata: inout std_logic_vector(20 downto 0)
);
end gpio_com;

architecture rtl of gpio_com is
	  -- Message and Data from GPIO
    --signal read_value : std_logic_vector(18 downto 0);
	 --signal write_value : std_logic_vector(15 downto 0);
	 signal ready, done : std_logic_vector(0 downto 0);
	  -- DE2 is reader = 1, DE2 is writer = 0
	 signal reader : std_logic_vector(0 downto 0) := "1";
begin
	 -- WHEN DE2 IS A READER (reader = 1):
	 -- serialdata = [Data][Message Type][Done][Ready]
	 --				  20 - 6    5 - 2        1		0
	 -- WHEN DE2 IS A WRITER (reader = 0):
	 -- serialdata = [Data][Ready][Done]
	 --              20 - 2   1     0
	 ready <= serialdata(0 downto 0); -- Get READY flag
	 serialdata(1 downto 1) <= done;  -- Set DONE flag
	 
	-- read_value <= serialdata(20 downto 2);
	 
    process (clk)
    begin
        if rising_edge(clk) then
            if (reset_n = '0') then
					 done <= "0";
					 reader <= "1";
				elsif(wr_en = '1' and addr = "00") then
					-- Setting the DONE flag
					done <= writedata(0 downto 0);
				elsif(wr_en = '1' and addr = "01") then
					-- Changing communication directions
					-- READY flag will become DONE, and
					-- DONE flag will become READY.
					reader <= writedata(0 downto 0);
				elsif(wr_en = '1' and addr = "10" and reader = "0") then
					-- Setting the DATA to transmit
					-- Since we are transmitting sound, only need 16 bits
					serialdata(17 downto 2) <= writedata(15 downto 0);
				end if;
        end if;
    end process;
    
    process (rd_en, addr)
    begin
        readdata <= (others => '-');
        if (rd_en = '1') then
				if (addr = "00") then
					 -- Read READY flag
					readdata <= "0000000000000000000000000000000" & ready;
            elsif (addr = "01" and reader = "1") then
					 -- Read [MSG TYPE][DATA]
                readdata <= "0000000000000" & serialdata(20 downto 2);
            end if;
        end if;
    end process;
end rtl;
s