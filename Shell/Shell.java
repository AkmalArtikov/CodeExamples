package shell;

import java.io.*;
import java.util.*;
/**
 *
 * @author Акмал
 */

public class Shell {
    public static String path;
    public static boolean is_console;
    

// Copying file method (other methods use it)
    public static boolean copyfile(File from, File to, String command) 
    {
        FileInputStream is = null;
        FileOutputStream os = null;
        try 
        {
            is = new FileInputStream(from);
            os = new FileOutputStream(to);
            int length;
            byte[] buf = new byte[10000];
            while (true) 
            {
                length = is.read(buf);
                if (length < 0) 
                {
                    break;
                }
                os.write(buf, 0, length);
            }
            if (is != null) 
            {
                is.close();
            }
            if(os != null)
            {
                os.close();
            }
            return true;
        } 
        catch (Exception excpt) 
        {
            System.err.println("Error: " + command + ": " + excpt.getMessage());
            if (!is_console) 
            {
                System.exit(1);
            }
        } 
        return false;
    }
    
//Command copy
    public static boolean copy(File from, File to, String command) 
    {
        File to2 = to;
        if (from.isFile()) 
        {
            if (!to.isFile() && (to.exists())) 
            {
                to2 = new File(to.getAbsolutePath() + "/" + from.getName());
            }
            if (!copyfile(from, to2, command)) 
            {    
                System.err.println("Error: can't "+command );
                if (!is_console) 
                {
                    System.exit(1);
                }
                return false;
            }
        } 
        else 
        {
            to2 = new File(to.getAbsolutePath() + "/" + from.getName());
            if ((!to2.exists() && !to2.mkdirs()) || !from.exists()) 
            {
                System.err.println("Error: can't " + command);
                if (!is_console) 
                {
                    System.exit(1);
                }
                return false;
            }
            for (String f : from.list()) 
            {
                File new_from = new File(from.getAbsolutePath() + "/" + f);
                File new_to = new File(to2.getAbsolutePath() + "/" + f);
                if (!copy(new_from, new_to, command)) 
                {
                    return false;
                }
            }    
        }
        return true;
    }
    
//Command delete directory
    public static boolean delete_directory(File directory) 
    {
        try 
        {
            if (directory.isDirectory()) 
            {
                String[] children = directory.list();
                for (String s : children) 
                {
                    File f = new File(directory, s);
                    if (!delete_directory(f)) 
                    {
                        return false;
                    }
                }
                return directory.delete();
            } 
            else 
            {
                return directory.delete();
            }
        } 
        catch (Exception excpt) 
        {
            System.err.println("Error: rm " + excpt.getMessage());
            if (!is_console) 
            {
                System.exit(1);
            }
        }
        return false;
    }
    
//Gets the number of commands
    public static boolean commands_number(ArrayList<String> args, int size) 
     {
        if (args.size() < size) 
        {
            if (!is_console) 
            {
                System.err.println("Error: command");
                System.exit(1);
            }
            return false;
        }
        return true;
    }
    
//Command move file
    public static boolean movefile(File from, File to) 
    {
        if (!copy(from, to, "mv")) 
        {
            return false;
        }
        if (!delete_directory(from)) 
        {
            System.err.println("Error: mv");
            if (!is_console) 
            {
                System.exit(1);
            }
            return false;
        }
        return true;
    }
    
//Parsing input information on commands
    public static ArrayList<String> parser(String s) 
    {
        ArrayList<String> comm = new ArrayList<String>();
        int start_new_comm = 0;
        boolean flag = false;
        for (int i = 0; i < s.length(); i++) 
        {
            char ch = s.charAt(i);
            if(ch == ' ')
            {
                if (!flag) 
                {
                    if (!s.substring(start_new_comm, i).replaceAll("\\s", "").isEmpty()) 
                    {
                        comm.add(s.substring(start_new_comm, i));
                    }
                    start_new_comm = i + 1;
                }
    //            break;
            }
            if(ch == '\"')
            {
                if (flag) 
                {
                    comm.add(s.substring(start_new_comm, i));
                } 
                flag = !flag;
                start_new_comm = i + 1;
    //            break;
            }        
        } 
        if (!s.substring(start_new_comm, s.length()).replaceAll("\\s", "").isEmpty()) 
        {
            comm.add(s.substring(start_new_comm, s.length()));
        }
        return comm;
    }
    
//Process existing commands
    public static boolean exist_command(String s)
    {
        switch (s.replaceAll("\\s+", "")) 
        {
            case "pwd":
                System.out.println(path);
                return true;
                
            case "dir":
                File directory = new File(path);
                for (String fl: directory.list()) 
                {
                    System.out.println(fl);
                }
                return true;
            case "exit":
                System.exit(0);
                return true;
                
        }
        ArrayList<String> args = parser(s);
        if (!commands_number(args, 2)) 
        {
            return false;
        }
        switch (args.get(0)) 
        {
            case "cd":
                switch (args.get(1)) 
                {
                    case "..":
                        try 
                        {
                            path = new File(path).getParentFile().getAbsolutePath();
                        } 
                        catch (Exception expt) 
                        {
                            System.err.println("Error: cd (root)");
                        }
                        break;
       
                    case ".":
                        break;
                    
                    default:
                        File new_path = new File(path + "/" + args.get(1));
                        File new_path2 = new File(args.get(1));
                        if (new_path.exists()) 
                        {
                            path = new_path.getAbsolutePath();
                        } 
                        else 
                        {
                            if (new_path2.exists()) 
                            {
                                path = new_path2.getAbsolutePath();
                            } 
                            else 
                            {
                                System.err.println("Error: cd");
                                if (!is_console) 
                                {
                                    System.exit(1);
                                }
                            }
                        }    
                        break;
                }
                return true;
            
            case "mkdir":
                File directory = new File(path + "/" + args.get(1));
                try 
                {
                    if (!directory.mkdir()) 
                    {
                        System.err.println("Error: mkdir " + directory);
                        if (!is_console) 
                        {
                            System.exit(1);
                        }
                    }
                } 
                catch (Exception expt) 
                {
                    System.err.println("Error: mkdir " + expt.getMessage());
                    if (!is_console) 
                    {
                        System.exit(1);
                    }
                }
                return true;
                
            case "rm":
                File file = new File(args.get(1));
                if (!file.isAbsolute()) 
                {
                    file = new File(path + "/" + file);
                }
                if (!delete_directory(file)) 
                {
                    System.err.println("Error: rm can't delete " + file);
                    if (!is_console)
                    {
                        System.exit(1);
                    }
                }
                return true;
                
            case "cp":
                if (!commands_number(args, 3)) 
                {
                    return false;
                }
                File from1 = new File(args.get(1));
                File from2 = new File(path + "/" + args.get(1));
                File to = new File(args.get(2));
                if (!to.isAbsolute()) 
                {
                	to = new File(path + "/" + args.get(2));
                }
                if (!from1.equals(to) && !from2.equals(to))
                {
                    if (!from1.exists()) 
                    {
                    	if (!from2.exists()) 
                        {
                            System.err.println("Error: cp \'" + from1.getAbsolutePath());
                            if (!is_console)
                            {
                                System.exit(1);
                            }
                        } 
                        else 
                        {
                            if (!to.isAbsolute()) 
                            {
                                to = new File(path + "/" + to);
                            }
                            if (!from1.isAbsolute()) 
                            {
                                from1 = new File(path + "/" + from1);
                            }
                            copy(from1, to, "cp");
                        }
                    } 
                    else 
                    {
                        if (!to.isAbsolute()) 
                        {
                           to = new File(path + "/" + to);
                        }
                        if (!from2.isAbsolute()) 
                        {
                            from2 = new File(path + "/" + from2);
                        }
                        copy(from2, to, "cp");
                    }
                }
                return true;
                
            case "mv":
                if (!commands_number(args, 2)) 
                {
                    return false;
                }
                File mv_from = new File(path + "/" + args.get(1));
                File mv_to = new File(path + "/" + args.get(2));
                if (!mv_from.exists()) 
                {
                	mv_from = new File(args.get(1));
                	if (!mv_from.exists()) 
                        {
                            System.err.println("Error: mv \'");
                            if (!is_console) 
                            {
                                System.exit(1);
                            }
                	}
                }
                File fullFrom = new File(mv_from.getAbsolutePath());
                File fullTo = new File(mv_to.getAbsolutePath());
                if (!mv_to.isAbsolute()) 
                {
                	fullTo = new File(path + "/" + mv_to);
                }
		try 
                {
                    if (fullFrom.getParentFile().equals(fullTo.getParentFile())) 
                    {
                        if (!mv_from.renameTo(mv_to)) 
                        {
                            movefile(fullFrom, fullTo);
                        }
                    } 
                    else 
                    {
                        movefile(fullFrom, fullTo);
                    }
                } 
                catch (Exception expt) 
                {
                    System.err.println("Error: mv" + expt.getMessage());
                    if (!is_console) 
                    {
                        System.exit(1);
                    }
                }
                return true;
                
            default:
                if (!is_console) 
                {
                    System.exit(1);
                }
                return false;
        } 
    }
    
    public static void main(String[] args) throws Exception
    {
        path =  new File("").getAbsolutePath();
        try 
        {
            if (args.length == 0) 
           {
                is_console = true;
                BufferedReader bf = new BufferedReader(new InputStreamReader(System.in));
                while (true) 
                {
                    System.out.print("$ ");
                    String commands[] = bf.readLine().split(";");          
                    for (String s : commands ) 
                    {
                        parser(s);
                        if (!exist_command(s)) 
                        {
                            System.err.println("Bad command \'"+ s + "\'");
                        }
                    }
                }
            } 
            else 
            {
                is_console = false;
                StringBuilder sb = new StringBuilder();
                for (String str : args) 
                {
                    sb.append(str).append(" ");
                }
                String commands[] = sb.toString().split(";");
                for (String s : commands) 
                {
                    exist_command(s);
                }
            }
        } 
        catch (Exception expt) 
        {
            System.err.println("Error - " + expt);
        }
    }
}
