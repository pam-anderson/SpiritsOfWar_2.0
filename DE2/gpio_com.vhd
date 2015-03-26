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
    signal saved_value : std_logic_vector(18 downto 0);
	-- signal message : std_logic_vector(4 downto 0);
	 signal ready, done : std_logic_vector(0 downto 0);
begin
	 -- serialdata = [Data][Message Type][Done][Ready]
	 --				  20 - 6    5 - 2        1		0
	 ready <= serialdata(0 downto 0);
	 saved_value <= serialdata(20 downto 2);
	 serialdata(1 downto 1) <= done;
	 
    process (clk)
    begin
        if rising_edge(clk) then
            if (reset_n = '0') then
					 done <= "0";
				elsif(wr_en = '1' and addr = "00") then
					done <= writedata(0 downto 0);
				end if;
        end if;
    end process;
    
    process (rd_en, addr, saved_value)
    begin
        readdata <= (others => '-');
        if (rd_en = '1') then
				if (addr = "00") then
					readdata <= "0000000000000000000000000000000" & ready;
            elsif (addr = "01") then
					 -- Send [MSG TYPE][DATA]
                readdata <= "0000000000000" & saved_value;
            end if;
        end if;
    end process;
end rtl;
