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
    signal saved_value : std_logic_vector(15 downto 0);
	 signal message : std_logic_vector(4 downto 0);
	 signal ready : std_logic_vector(0 downto 0);
begin
	 -- serialdata = [Data][Message Type][Ready]
	 --				  21 - 6    5 - 1        0
	 ready <= std_logic_vector(serialdata(0 downto 0));
	 
    process (clk)
    begin
        if rising_edge(clk) then
            if (reset_n = '0') then
                saved_value <= (others => '0');
					-- serialdata(0 downto 0) <= "0";
  			 end if;
        end if;
    end process;
    
    process (rd_en, addr, saved_value)
    begin
        readdata <= (others => '-');
        if (rd_en = '1') then
            if ((addr = "01") and (ready = "1")) then
					 -- Send [MSG TYPE][DATA]
                readdata <= "000000000000" & serialdata(20 downto 1);
					 -- Clear ready flag	
					 serialdata(0 downto 0) <= "1";
            end if;
        end if;
    end process;
end rtl;
